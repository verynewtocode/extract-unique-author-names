$path = "C:\Users\yilin\Documents\fcp\data\pypi_items.json"
$n = 1000

$reader = [System.IO.StreamReader]::new($path)
$buffer = New-Object char[] $n

$count = $reader.Read($buffer, 0, $n)
$reader.Close()

$text = [string]::new($buffer, 0, $count)
$text | Set-Clipboard