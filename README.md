<p align="center">
  <img src="assets/header.gif" width="800" alt="Cena em pixel art: noite em Belém, com lua, Ver-o-Peso, açaizeiros e uma canoa no rio. Texto: olá, mundo · estudante · IoT · IA · Belém, PA">
</p>

<p align="center">
  <img src="assets/divider.gif" width="800" alt="">
</p>

### `sobre_mim.ino`

```cpp
// Belém, PA · Estácio Belém · 2º semestre

struct Foco {
  const char* hardware = "ESP32, Arduino, sensores";
  const char* software = "C++, web (HTML/CSS/JS/PHP)";
  const char* ia       = "modelos locais com Ollama";
};

void setup() {
  Serial.begin(115200);
  Serial.println("olá, mundo");
}

void loop() {
  aprender();
  prototipar();
  documentar();   // o que funciona e o que quebrou
}
```

<p align="center">
  <img src="assets/divider.gif" width="800" alt="">
</p>

### `em_destaque.log`

<p align="center">
  <img src="assets/pulse.gif" width="800" alt="Animação: ESP32 ligado a um MPU6050, osciloscópio mostra o sinal de aceleração, pico acima do limiar, status muda para queda detectada e depois alerta enviado">
</p>

**Detector de queda para idosos.** O ESP32 lê a aceleração do MPU6050 e procura o padrão de uma queda: queda livre, impacto acima do limiar e depois imobilidade. Quando o padrão se completa, ele envia um alerta.

<sub>* A animação é ilustrativa. Não mostra leitura real do sensor.</sub>

<p align="center">
  <img src="assets/divider.gif" width="800" alt="">
</p>

### `serial_monitor`

<table>
  <tr>
    <td width="140" align="center"><img src="assets/icon_queda.gif" width="128" alt=""></td>
    <td>
      <b>Detector de queda</b><br>
      ESP32 + MPU6050 + IA para identificar quedas e avisar quem cuida.<br>
      <code>ESP32</code> <code>C++</code> <code>MPU6050</code>
    </td>
  </tr>
  <tr>
    <td width="140" align="center"><img src="assets/icon_roda.gif" width="128" alt=""></td>
    <td>
      <b>Roda de palavras</b><br>
      Seleção de palavras com joystick e sugestões contextuais.<br>
      <code>Arduino</code> <code>joystick</code> <code>IA</code>
    </td>
  </tr>
  <tr>
    <td width="140" align="center"><img src="assets/icon_inventario.gif" width="128" alt=""></td>
    <td>
      <b>Sistema de inventário</b><br>
      Cadastro e controle de itens pela web.<br>
      <code>HTML</code> <code>CSS</code> <code>JS</code> <code>PHP</code>
    </td>
  </tr>
</table>

<p align="center">
  <img src="assets/divider.gif" width="800" alt="">
</p>

### `ferramentas.h`

<p align="center">
  <img src="https://img.shields.io/badge/ESP32-150F26?style=flat-square&logo=espressif&logoColor=A78BFA" alt="ESP32">
  <img src="https://img.shields.io/badge/Arduino-150F26?style=flat-square&logo=arduino&logoColor=A78BFA" alt="Arduino">
  <img src="https://img.shields.io/badge/C++-150F26?style=flat-square&logo=cplusplus&logoColor=A78BFA" alt="C++">
  <img src="https://img.shields.io/badge/HTML-150F26?style=flat-square&logo=html5&logoColor=A78BFA" alt="HTML">
  <img src="https://img.shields.io/badge/CSS-150F26?style=flat-square&logo=css&logoColor=A78BFA" alt="CSS">
  <img src="https://img.shields.io/badge/JavaScript-150F26?style=flat-square&logo=javascript&logoColor=A78BFA" alt="JavaScript">
  <img src="https://img.shields.io/badge/PHP-150F26?style=flat-square&logo=php&logoColor=A78BFA" alt="PHP">
  <img src="https://img.shields.io/badge/Blender-150F26?style=flat-square&logo=blender&logoColor=A78BFA" alt="Blender">
  <img src="https://img.shields.io/badge/Pop!__OS-150F26?style=flat-square&logo=popos&logoColor=A78BFA" alt="Pop!_OS">
  <img src="https://img.shields.io/badge/Git-150F26?style=flat-square&logo=git&logoColor=A78BFA" alt="Git">
  <img src="https://img.shields.io/badge/Obsidian-150F26?style=flat-square&logo=obsidian&logoColor=A78BFA" alt="Obsidian">
  <img src="https://img.shields.io/badge/Ollama-150F26?style=flat-square&logo=ollama&logoColor=A78BFA" alt="Ollama">
</p>

### `contato`

<p align="center">
  <a href="https://www.linkedin.com/in/maykewendrell/"><img src="https://img.shields.io/badge/LinkedIn-150F26?style=flat-square&logo=linkedin&logoColor=A78BFA" alt="LinkedIn"></a>
  <a href="mailto:maykewendrell2@gmail.com"><img src="https://img.shields.io/badge/E--mail-150F26?style=flat-square&logo=gmail&logoColor=A78BFA" alt="E-mail"></a>
  <a href="https://www.instagram.com/maykilovy/"><img src="https://img.shields.io/badge/Instagram-150F26?style=flat-square&logo=instagram&logoColor=A78BFA" alt="Instagram"></a>
</p>

<p align="center">
  <img src="assets/footer.gif" width="800" alt="Rio à noite com canoa e a mensagem: obrigado pela visita">
</p>
