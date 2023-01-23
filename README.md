# About: Genetic Backtest & Auto-Pilot Trading Algorithm 
### I'm too lazy to descrive what I built so, I created an simple image using Figma.   
 
As you can see, this app is way too complicated.🤯🤮 
Therfore, I will refactor into microservices using k8s 🐳

## Refactoring plan for a monolith into microservices ♻️

#### 📈 Strategy Algorithm Provider API 📈 
<details>
<summary>Submit: "Strategy ID & Parameter" 
  <br> &emsp;↪️&nbsp;Return: "Starategy Logic & Parameter"</summary>
This API provides exactly same trading strategy logic to backtester and trading system by their post requests. So that they can run backtest and trade systems under the same condition⚔️
</details>
  
  
#### 🔁 Genetic Backtesting Algorithm API 🔁 
<details>
<summary>Submit: "Strategy Logic & Parameter" 
  <br> &emsp;↪️&nbsp;Return: Returns "The Most Profitable Backtest Parametor"</summary>
Send POST request to run genetic backtest algorithm according to posted strategy and parameters. Results will be stored to Central Database (maybe some cloud storage like GCS). Planning to directry send post request to Trading Algo API to start trading according to the backtest result🦠
</details>


#### 💱 Genetic Autopilot Trading Algorithm API 💱 
<details>
<summary>Submit: A  
  <br> &emsp;↪️&nbsp;Return:   B</summary>
  🧬🧬🧬🧬
</details>

#### 🏦 Account Custody Webhook 🏦 
<details>
<summary>Submit: "None" 
  <br> &emsp;↪️&nbsp;Return:  "Account Data"</summary>
  Collects account data from all of exchanges and bank accounts. Such as Trading History & Balance/PNL & Position. It store them to 🩺 
</details>

  
#### 🕋 Central Database API 🕋
<details>
<summary>Submit:A  
  <br> &emsp;↪️&nbsp;Return: B</summary>
  Stores backtest result data, trading data, active session(trade/backtest) info, account balnace data, exception data, backups and so on...🧐 
</details>
  
#### 🔮 User Interface 🔮 
<details>
<summary> Controll and Moniter Everything in One Place.</summary>
⚙️
</details>

 
