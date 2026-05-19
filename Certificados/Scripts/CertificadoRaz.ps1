$cert = New-SelfSignedCertificate -Type Custom `
-Subject "CN=zpac.as" `
-KeyAlgorithm RSA -KeyLength 2048 -KeySpec Signature -KeyExportPolicy Exportable `
-KeyUsageProperty All -KeyUsage None `
-Provider "Microsoft Enhanced RSA and AES Cryptographic Provider" `
-NotBefore (Get-Date) `
-NotAfter (Get-Date).AddYears(10) `
-HashAlgorithm sha256 `
-TextExtension @("2.5.29.19={critical}{text}ca=1") `
-CertStoreLocation "Cert:\CurrentUser\My"