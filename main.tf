# Manisa Celal Bayar Universitesi - Bulut Bilisim ve Siber Guvenlik
# Ogrenci: Hikmet Emre Gultekin - 2516016024
# IaC (Infrastructure as Code) - Serverless Guvenlik Altyapisi

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# 1. Kaynak Grubu
resource "azurerm_resource_group" "rg_threat" {
  name     = "rg-threat-dashboard-prod"
  location = "westeurope"
  tags = {
    Environment = "Production"
    Project     = "ThreatDataPipeline"
    Student     = "HikmetEmreGultekin"
  }
}

# 2. Statik Web Arayuzu Hosting (Zararli URL tiklanmasini engelleyen guvenli alan)
resource "azurerm_static_site" "web_dashboard" {
  name                = "threat-dashboard-ui"
  resource_group_name = azurerm_resource_group.rg_threat.name
  location            = azurerm_resource_group.rg_threat.location
  sku_tier            = "Free" # 0 TL Maliyet Hedefi
}

# 3. Izole Serverless Fonksiyon Alani (URL Defang ve Boyut Denetimi)
resource "azurerm_service_plan" "asp_serverless" {
  name                = "asp-serverless-defang"
  resource_group_name = azurerm_resource_group.rg_threat.name
  location            = azurerm_resource_group.rg_threat.location
  os_type             = "Linux"
  sku_name            = "Y1" # Tuketim plani (Free Tier)
}

# 4. Butce ve Maliyet Alarmi (Hedef: 0 TL / Asim Uyarisı)
resource "azurerm_consumption_budget_resource_group" "budget_alarm" {
  name              = "budget-zero-cost-alert"
  resource_group_name = azurerm_resource_group.rg_threat.name
  amount            = 1.0 # 1 USD/EUR ulasinca alarm ver
  time_grain        = "Monthly"

  time_period {
    start_date = "2026-10-01T00:00:00Z"
  }

  notification {
    enabled        = true
    threshold      = 80.0
    operator       = "GreaterThan"
    contact_emails = ["2516016024@cbu.edu.tr"]
  }
}