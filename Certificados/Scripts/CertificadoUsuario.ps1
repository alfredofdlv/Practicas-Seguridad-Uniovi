New-SelfSignedCertificate -Type Custom `
-Subject "CN=zpusu.as" -DnsName "zpusu.as” `
-KeyAlgorithm RSA -KeyLength 2048 -KeySpec KeyExchange -KeyExportPolicy Exportable `
-KeyUsageProperty All -KeyUsage None `
-Provider "Microsoft Enhanced Cryptographic Provider v1.0" `
-NotBefore (Get-Date) `
-NotAfter (Get-Date).AddYears(5) `
-HashAlgorithm sha256 `
-Signer $cert `
-CertStoreLocation "Cert:\CurrentUser\My"
