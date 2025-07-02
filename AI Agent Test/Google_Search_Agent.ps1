
# Prompt user for input
$searchSubject = Read-Host -Prompt "Enter the search subject (e.g., Tesla)"
$adverseKeywordsInput = Read-Host -Prompt "Enter adverse keywords separated by commas (e.g., fraud,law suit)"
$adverseKeywords = $adverseKeywordsInput -split "\s*,\s*"

# Prepare headers
$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("openapi", "true")
$headers.Add("Tenant", "flow-demo-us1")
$headers.Add("Authorization", "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJaYlZ1X1drWUtROGFlNTVXYm8xYnZRZ2w4TEg2Mkd3YUVKbTlpN3B4TlI4In0.eyJleHAiOjE3NTE0NTM4MjIsImlhdCI6MTc1MTQ1MjAyMiwiYXV0aF90aW1lIjoxNzUxNDUxOTQ5LCJqdGkiOiIxZmI5ZjA1Mi01YThkLTQxMzMtOTI5My03OGEzZTI3YmU3MTciLCJpc3MiOiJodHRwczovL2dlbmFpLXdvcmtmbG93cy11czEta2V5Y2xvYWsuc3ltcGhvbnlhaS5kZXYvcmVhbG1zL2Zsb3ctZGVtby11czEiLCJhdWQiOlsid29ya2Zsb3ctY2FudmFzLWJhY2tlbmQiLCJhY2NvdW50Il0sInN1YiI6IjA0MWNiNWU2LTNlNTYtNDkyMi05YjVkLTY1MzY2NTEzODAwMyIsInR5cCI6IkJlYXJlciIsImF6cCI6ImZsb3ctZGVtby11czEiLCJzaWQiOiI2NGM0YzFmMS1iZjA0LTQ4OWItYTIwZC03ZjY0NDhhMzUwNTIiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vZ2VuYWktd29ya2Zsb3dzLXVzMS5zeW1waG9ueWFpLmRldiIsImh0dHBzOi8vZ2VuYWktd29ya2Zsb3dzLXVzMS1rZXljbG9hay5zeW1waG9ueWFpLmRldiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtZmxvdy1kZW1vLXVzMSJdfSwicmVzb3VyY2VfYWNjZXNzIjp7IndvcmtmbG93LWNhbnZhcy1iYWNrZW5kIjp7InJvbGVzIjpbIjYyNzBlMGJmLWUyZjEtNGE2MS1iNDEyLTk5OWNhNTgwNGUxY19wcm9qZWN0X2FkbWluIiwid29ya3NwYWNlX2NvbGxhYm9yYXRvciIsIjhjNzE0ZDBlLWJlYWQtNDkyOC1hMzhiLTYxODQxOWFkNjQwNF9wcm9qZWN0X2FkbWluIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJZb3Vzc2VmIFNheWVnaCIsInByZWZlcnJlZF91c2VybmFtZSI6InlvdXNzZWYuc2F5ZWdoQHN5bXBob255YWkuY29tIiwiZ2l2ZW5fbmFtZSI6IllvdXNzZWYiLCJmYW1pbHlfbmFtZSI6IlNheWVnaCIsImVtYWlsIjoieW91c3NlZi5zYXllZ2hAc3ltcGhvbnlhaS5jb20ifQ.X0D1VBY1pfA1qPUJmfXkGLMhrm0Su1KG-9oETC8fztlIBAbZF83sQIn8TbjpVVs-cuNoRIrI0HvHyzTegF2d7zaDCjEEv6-cKuVPHVwTkZ2e1cWOxVPkV3Lr54oOxxXkqvAoPWYe6S1OrUnidcj5XwlMSI9tgsAUUp-6hQl2Os6dOujNGLB0f29BnCh2RyXT8595wht111vY1YhxHdRshXPKvYO6KIrMDSj_VYvkkbBNxX5BSRvKktZHy3Ztk9snDg19Iq29aV_yNdM3llyAdAb40OaXGO7h6yvs7VOcce8_GOtNZYfS0Kl7cNr4eS2Keq6UdnWQ0maGjkHdljPGmA")
$headers.Add("Content-Type", "application/json")

# Prepare body
$body = @{
    search_subject   = $searchSubject
    adverse_keywords = $adverseKeywords
    Empty_list       = @()
    html_output      = $true
} | ConvertTo-Json -Depth 10

# Send request
$response = Invoke-RestMethod -Uri "https://genai-workflows-us1.symphonyai.dev/webhook-service/release/0.0.0/webhook/13f88fa7-1102-41fe-835c-b569aab108da" -Headers $headers -Method Post -Body $body

# Print response
$response | ConvertTo-Json

# Pause before exit
Read-Host -Prompt "Press Enter to exit"
