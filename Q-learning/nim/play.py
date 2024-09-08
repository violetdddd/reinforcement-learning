from nim import train, play

# Train an AI by playing 10000 games against itself
ai = train(10000)  

# choose human's order randomly
play(ai)  
