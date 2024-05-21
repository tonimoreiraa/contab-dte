Import-Module PKI
$diretorio = "C:\Users\nataniel\Downloads\CERTIFICADOS\CERTIFICADOS"

function Install-Certificates {
    param (
        [array]$certificates
    )

    foreach ($arquivoPFX in $certificates) {
        $nomeCertificado = $arquivoPFX.BaseName.Split(" ")[0..($arquivoPFX.BaseName.Split(" ").Count - 2)] -join " "
        $senhaCertificado = $arquivoPFX.BaseName.Split(" ")[-1]
        $pass = ConvertTo-SecureString -String $senhaCertificado -AsPlainText -Force

        try {
            Import-PfxCertificate -FilePath $arquivoPFX.FullName -CertStoreLocation "Cert:\CurrentUser\My" -Password $pass -Exportable
            Write-Host "Certificado '$nomeCertificado' com senha $senhaCertificado instalado com sucesso."
        }
        catch {
            Write-Host "Erro ao instalar o certificado '$nomeCertificado': $_"
        }
    }
}

function Run-PythonScript {
    param (
        [string]$scriptPath
    )

    $process = Start-Process -FilePath "python" -ArgumentList $scriptPath -NoNewWindow -PassThru
    $process.WaitForExit()

    return $process.ExitCode
}

$arquivosPFX = Get-ChildItem -Path $diretorio -Filter *.pfx
$batchSize = 6

for ($i = 0; $i -lt $arquivosPFX.Count; $i += $batchSize) {
    $batch = $arquivosPFX[$i..([math]::Min($i + $batchSize - 1, $arquivosPFX.Count - 1))]

    Install-Certificates -certificates $batch

    $exitCode = Run-PythonScript -scriptPath "C:\Users\nataniel\Desktop\AutomacoesDPI\contab-dte-main\main.py"

    Write-Host "Python script exited with code $exitCode."

    Get-ChildItem -Path Cert:\CurrentUser\My | Remove-Item
}