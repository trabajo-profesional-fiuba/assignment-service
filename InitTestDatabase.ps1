Param(
    [switch]
    $StopDatabase
)



function IsDockerInstalled(){
    if(Get-Command docker){
        Write-Host "Docker installed: "-NoNewline; Write-Host -ForegroundColor Green "Yes"
        return $true
    }

    Write-Host "Docker installed: "-NoNewline; Write-Host -ForegroundColor Red "No"
    Write-Host "Please install docker from: https://www.docker.com/"
    
    return $false
}


if (IsDockerInstalled){
    
    if (!$StopDatabase) {
        Write-Host "Starting PostgreSQL 15 container..."
    
        docker run -d --rm `
        -e POSTGRES_USER=postgres `
        -e POSTGRES_PASSWORD=postgres `
        -e POSTGRES_DB=postgres `
        -p 5433:5432 `
        --name postgres `
        postgres:15
    
        $postgresUrl = "postgres://postgres:postgres@localhost:5433/postgres"
    
        Write-Host "PostgreSQL container started."
        Write-Host -ForegroundColor Yellow "Container information"
        Write-Host  "Detached mode on"
        Write-Host  "Username: postgres"
        Write-Host  "Password: postgres"
        Write-Host  "Database: postgres"
        Write-Host  "Ports: 5433:5432"
    
        Write-Host -ForegroundColor Cyan "URL Connection: $postgresUrl"
    }
    else {
        Write-Host "Stopping and removing PostgreSQL 15 container..."
        $_ = docker stop postgres
    }
}
