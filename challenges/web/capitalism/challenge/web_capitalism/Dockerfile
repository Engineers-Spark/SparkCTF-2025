
FROM golang AS builder
WORKDIR /app
COPY . .
RUN go mod download
RUN CGO_ENABLED=0 GOOS=linux go build -o ctf-app .
FROM scratch
COPY --from=builder /app/ctf-app /ctf-app
COPY flag.txt /
EXPOSE 8080
USER 1000
CMD ["/ctf-app"]