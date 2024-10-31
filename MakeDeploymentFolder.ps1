# Este script es utilizado para realizar los deployments en Azure
# Para eso, primero debemos crear una carpeta temporal y luego eliminarla manualmente
# En esta carpeta vamos a agregar todos los archivos necesarios para correr la aplicacion
# dejando sin mover configuraciones, git, readme, tests, etc.


# Ademas, antes de correr, es importante tener en cuenta que necesitamos
# que start_app.sh tenga Unix-Style line endings (LF) que al programar en Windows se cambia a DOS-style line endings (CRLF)
# En algun momento, podemos probar con https://just.systems/man/en/introduction.html y ver si nos funciona

Param(
    [string]
    [Parameter(HelpMessage = "Indicate the enviroment", Mandatory = $true)]
    [ValidatePattern("(staging|prod)")]
    $Enviroment
)

function Dos2Unix {

    $filePath = "start_app.sh"
    $fileContent = Get-Content -Raw -Path $filePath

    $fileContent = $fileContent -replace "`r", ""

    Set-Content -Path $filePath -Value $fileContent
}

function InstallAndExportDependencies {
    Write-Host "Locking dependencies with Poetry..."
    Invoke-Expression -Command "poetry lock"
    
    Write-Host "Installing dependencies with Poetry..."
    Invoke-Expression -Command "poetry install"
    
    Write-Host "Exporting dependencies to requirements.txt..."
    Invoke-Expression -Command "poetry export -f requirements.txt --output requirements.txt"
    
    Write-Host "Dependencies have been locked, installed, and exported successfully."
}


function MakeFolder {
    param (
        [string]$Environment
    )

    if ($Environment -eq 'staging') {
        $env = '.env.staging'
    }
    elseif ($Environment -eq 'prod') {
        $env = '.env.production'
    }
    else {
        Write-Error "Invalid environment specified"
        return
    }

    $ItemsToCopy = @('src', 'alembic', 'alembic.ini', 'start_app.sh', 'main.py', 'requirements.txt', $env, '.deployment')
    $buildPath = "Build"

    
    if (-Not (Test-Path -Path $buildPath)) {
        New-Item -Path $buildPath -ItemType Directory
    }
    else {
        Remove-Item -Path $buildPath -Recurse
    }

    foreach ($Item in $ItemsToCopy) {
        Write-Host "Copying $Item to $buildPath"
        Copy-Item -Path $Item -Destination $buildPath -Recurse -Exclude "*.pyc"
    }

    Write-Host "All specified items have been copied to the $buildPath directory."
}


#Dos2Unix
InstallAndExportDependencies
MakeFolder $Enviroment