import streamlit as st
import matplotlib.pyplot as plt
from game import *

st.title("El juego de la Perinola")

st.markdown('''```
Alexander Baquiax
12007988
```''')

st.write("\n\n\n")

play, montecarlo = st.tabs(["💰 :orange[¡A jugar!]", "📈 :orange[Simulación Montecarlo]"])

with play:
    st.write("Este es un juego de la perinola, donde se puede jugar con 2 a 10 jugadores.")
    st.write("Para simular el juego, se debe ingresar el número de jugadores y el dinero inicial de cada jugador.")

    ## Get total number of players
    n_players = st.number_input("Número de jugadores", min_value=2, max_value=100, value=10, step=1)

    ## Get intitial money
    initial_money = st.number_input("Dinero inicial", min_value=1.0, max_value=1000.0, value=10.0, step=1.0)

    ## button to start game
    if st.button("▶️ Simular juego"):
        with st.spinner('Procesando'):
            ## create game
            spinner = SpinnerGame(n_players, initial_money)

            ## play game
            while spinner.winner is None:
                spinner.spin()        

            st.info(f"El ganador es el :green[**# {spinner.winner.name}**] con :orange[**${spinner.winner.money}**] restantes, luego de :red[**{spinner.spins}**] giros")


            lost = []
            gained = []
            for player in spinner.all_players:
                lost.append(player.lost)
                gained.append(player.gained)

            ## plot results
            fig, ax = plt.subplots()
            ax.bar(range(1, n_players + 1), lost, label="Perdido")
            ax.bar(range(1, n_players + 1), gained, bottom=lost, label="Ganado")
            ax.set_ylabel("Dinero")
            ax.set_xlabel("Jugadores")
            ax.set_title("Dinero ganado y perdido por jugador")
            ax.legend()
            st.pyplot(fig)

with montecarlo:
    ## Get total number of players
    n_players = st.number_input("Número de jugadores", min_value=2, max_value=100, value=10, step=1, key="m_n_players")

    ## Get intitial money
    initial_money = st.number_input("Dinero inicial", min_value=1.0, max_value=1000.0, value=5.0, step=1.0, key="m_initial_money"  )

    simulations = st.number_input("Número de simulaciones", min_value=1, max_value=1000, value=250, step=1)

    if st.button("▶️ Ejecutar simulaciones"):
        with st.spinner('Calculando...'):
            winner_spins = 0
            loser_spins = 0
            spins_to_win = []

            for i in range(simulations):
                spinner = SpinnerGame(players=n_players, initial_momeny=initial_money)

                while spinner.winner is None:
                    spinner.spin()
                    winner_spins += 1
                    

                loser_spins += len(spinner.first_broken.history)


            avg_winner = winner_spins / simulations
            avg_loser = loser_spins / simulations        
            
            for i in range(2, n_players + 1):
                avg_spins = 0
                for _ in range(simulations):
                    spinner = SpinnerGame(players=i, initial_momeny=initial_money)

                    while spinner.winner is None:
                        spinner.spin()
                    
                    avg_spins += spinner.spins
                
                avg_spins /= simulations
                
                spins_to_win.append(avg_spins)
            

            st.info(f"El promedio de giros para que haya un ganador es de :orange[**{avg_winner}**]")
            st.info(f"El promedio de giros para que salga el primer jugador es de :red[**{avg_loser}**]")

            fig, ax = plt.subplots()
            ax.plot(range(2, n_players + 1), spins_to_win)
            ax.scatter(range(2, n_players + 1), spins_to_win)
            ax.set_ylabel("AVG giros")
            ax.set_xlabel("Cantidad de jugadores")
            ax.set_title(f"Promedio de giros para ganar con {initial_money} de dinero inicial")
            st.pyplot(fig)
