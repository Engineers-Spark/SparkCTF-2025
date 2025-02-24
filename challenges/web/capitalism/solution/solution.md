
This challenge exploits an inconsistency in how large numbers are decoded by different JSON parsers. Specifically, the `jsonparser` library used in the application does not handle extremely large numbers correctly, causing them to be truncated or converted to `0`. This behavior can be leveraged to bypass authentication mechanisms that rely on numeric input validation.


1. **Application Behavior**:
   - The application uses two libraries for JSON parsing:
     - `encoding/json`: Used for standard JSON unmarshaling.
     - `github.com/buger/jsonparser`: Used for faster, low-level JSON parsing.
   - When a very large number (e.g., `999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999`) is passed as the `employee_id`, the `jsonparser.GetInt` function truncates it to `0`.

2. **Exploitation**:
   - By sending a POST request to `/login` with an excessively large `employee_id`, the application interprets it as `0`, which corresponds to the `admin` role in the `employeeDB` map.
   - Once authenticated as an admin, the attacker can exploit the Local File Inclusion (LFI) vulnerability in the `/files` endpoint to read sensitive files, such as the flag.
