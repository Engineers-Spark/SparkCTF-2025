package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math/rand"
	"net/http"
	"time"

	"github.com/buger/jsonparser"
	"github.com/golang-jwt/jwt/v5"
)

const (
	adminPassword = "24398637a3758fb6bb69d82b7edd558d"
	jwtSecretKey  = "92d25af76e5abc74a141a03e9ed0faf4"
)

var employeeDB = map[int]string{
	1: "guest",
	2: "employee",
	0: "admin",
}

func main() {
	http.HandleFunc("/login", loginHandler)
	http.HandleFunc("/files", filesHandler)
	if err := http.ListenAndServe(":8080", nil); err != nil {
		panic(err)
	}
}

func loginHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body", http.StatusBadRequest)
		return
	}
	var input map[string]interface{}
	if err := json.Unmarshal(body, &input); err != nil {
		http.Error(w, "Invalid JSON payload", http.StatusBadRequest)
		return
	}
	if id, ok := input["employee_id"]; ok {
		if id == float64(0) {
			password, _ := input["password"].(string)
			if password == adminPassword {
				token := generateJWT(0, "admin")
				http.SetCookie(w, &http.Cookie{
					Name:  "auth_token",
					Value: token,
					Path:  "/",
				})
				fmt.Fprintln(w, "Admin login successful.")
				return
			} else {
				http.Error(w, "Invalid password for admin access", http.StatusForbidden)
				return
			}
		}
	}

	employeeID, _ := jsonparser.GetInt(body, "employee_id")

	if employeeID < 0 {
		http.Error(w, "Employee ID cannot be negative", http.StatusBadRequest)
		return
	}

	employeeIDInt := int(employeeID)
	role, exists := employeeDB[employeeIDInt]
	if !exists {
		employeeIDInt = rand.Intn(9999) + 1
		role = "guest"
	}
	token := generateJWT(employeeIDInt, role)
	http.SetCookie(w, &http.Cookie{
		Name:  "auth_token",
		Value: token,
		Path:  "/",
	})
	fmt.Fprintf(w, "Login successful. Assigned role: %s, Employee ID: %d", role, employeeIDInt)
}


func filesHandler(w http.ResponseWriter, r *http.Request) {
	cookie, err := r.Cookie("auth_token")
	if err != nil {
		http.Error(w, "Unauthorized access. Please login first.", http.StatusUnauthorized)
		return
	}
	token, err := jwt.Parse(cookie.Value, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return []byte(jwtSecretKey), nil
	})
	if err != nil || !token.Valid {
		http.Error(w, "Invalid or expired token", http.StatusUnauthorized)
		return
	}
	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok {
		http.Error(w, "Invalid token claims", http.StatusUnauthorized)
		return
	}
	role := claims["role"].(string)
	employeeID := claims["employee_id"].(float64)
	if role == "admin" {
		file := r.URL.Query().Get("file")
		if file == "" {
			http.Error(w, "File parameter is missing", http.StatusBadRequest)
			return
		}
		data, err := ioutil.ReadFile(file)
		if err != nil {
			http.Error(w, "Error reading file", http.StatusInternalServerError)
			return
		}
		w.Write(data)
		return
	}
	if role == "guest" {
		http.Error(w, fmt.Sprintf("Guests cannot access files. Employee ID: %d", int(employeeID)), http.StatusForbidden)
		return
	}
	http.Error(w, "Invalid role. Please login again.", http.StatusUnauthorized)
}

func generateJWT(employeeID int, role string) string {
	claims := jwt.MapClaims{
		"employee_id": employeeID,
		"role":        role,
		"exp":         time.Now().Add(time.Hour * 1).Unix(),
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	signedToken, err := token.SignedString([]byte(jwtSecretKey))
	if err != nil {
		panic(err)
	}
	return signedToken
}
