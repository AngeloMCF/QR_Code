# QR_Code
 
Criado com a finalidade de gerar QR Codes de uma url passada ou de uma rede de WIFI para facilitar o compartilhamento da mesma.

## Estrutura de uma URL de endereço WIFI
```
WIFI:S:<SSID>;T:WPA<ENCRYPTION_TYPE>;P:<KEY>;H:<HIDDEN_SSID(true/false)>;
^    ^        ^                      ^       ^
|    |        |                      |       +-- hidden SSID (true/false)
|    |        |                      +-- WPA KEY       
|    |        +-- encryption type       
|    +-- ESSID       
+-- Code Type   
```

Exemplo de URL WIFI: `WIFI:S:RedeTeste;T:WPA;P:SenhaModelo@;H:false;`

 - Nome da rede: `RedeTeste`
 - Senha: `SenhaModelo@`
 - Rede Oculta?: `Não`

QR Code Gerado

<img src='./QRCode_WI-FI-RedeTeste.png' style="height:200px">
 