New-SelfSignedCertificate -Type Custom `
-Subject "CN=zpser.as" -DnsName "zpser.as", "www.zpser.es", "www.zpser.com" `
-KeyAlgorithm RSA -KeyLength 2048 -KeySpec KeyExchange -KeyExportPolicy Exportable `
-KeyUsageProperty All -KeyUsage None `
-Provider "Microsoft Enhanced RSA and AES Cryptographic Provider" `
-NotBefore (Get-Date) `
-NotAfter (Get-Date).AddYears(5) `
-HashAlgorithm sha256 `
-Signer $cert `
-CertStoreLocation "Cert:\CurrentUser\My"