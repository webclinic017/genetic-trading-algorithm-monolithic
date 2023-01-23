# About: Genetic Backtest & Auto-Pilot Trading Algorithm 
##### I'm too lazy to descrive what I built so, I created an simple image using Figma.   
 
As you can see, this app is way too complicated.🤯🤮 
Therfore, I will refactor into microservices using k8s 🐳

## Refactoring plan for a monolith into microservices ♻️

#### 📈 Strategy Algorithm Provider API 📈 
<details>
<summary>Details🧾</summary>
Submit: "Strategy ID & Parameter" <br>Return: "Starategy Logic & Parameter" <br><br> 
This API provides exactly same trading strategy logic to backtester and trading system by their post requests. So that they can run backtest and trade systems under the same condition⚔️
</details>  

  
#### 🧬 Genetic Backtesting Algorithm API 🧬 
<details>
<summary>🧾</summary>
Submit: "Strategy Logic" & "Backtest Parameter" <br> Return: "Trading Parameter (The Most Profitable Parametor)" <br> <br>
Send POST request to run genetic backtest algorithm according to submitted strategy and parameters. Results will be stored to Central Database (maybe some cloud storage like GCS). Planning to directry send post request to Trading Algo API to start trading according to the backtest result🦠
</details>


#### 💱 Genetic Autopilot Trading Algorithm API 💱 
<details>
<summary>🧾</summary>
Submit: "Trading Parameter" & "Strategy" <br> Return: "None" <br> <br>
This app auto trade according to requested strategy and params. If this app got request, it stores to params to database. The database immidiatery notice that params were added. Then it starts trading session. This app is capable of manage multiple proccess running and storing trading information to the database. This trading system is very complicated. I might need to change the structrure. Anyway, I need more space to finish explaination...
</details>

#### 🔶 Account Custody Webhook 🔶
<details>
<summary>🧾</summary>
Submit: "None" <br> Return: "Account Data" <br> <br>
Collects account data from all of exchanges and bank accounts. Such as Trading History & Balance/PNL & Position. It store them to 🩺 
</details>

  
#### 🕋 Central Database API 🕋
<details>
<summary>🧾</summary>
Submit:A <br> Return: B <br><br>
Stores backtest result data, trading data, active session(trade/backtest) info, account balnace data, exception data, backups and so on...🧐 
</details>
  
#### 🔮 Trading User Interface 🔮 
<details>
<summary>Details🧾</summary>
Controll and Moniter Everything in One Place. ⚙️
</details>

 
