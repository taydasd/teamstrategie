const gameTime = 600; // 10 Mins
let gameStopped = true;

setInterval(() => {
    fetch("state").then((res) => res.json().then((json) => {
        setScores(json.playerScore, json.botScore);
    }))
}, 500);

function setScores(playerScore, botScore)
{
    const playerIncrement = playerScore - playerScoreField.value;
    const botIncrement    = botScore    - botScoreField.value;

    if (playerIncrement > 0 || botIncrement > 0) {
        let playerLead = playerScore - botScore;

        if (playerLead < -2 && botIncrement > 0) {
            godlikeAudio.play();
            playGIF('bot');
        } else if (playerLead > 2 && playerIncrement > 0) {
            unstoppableAudio.play();
            playGIF('prof');
        }
    }
    playerScoreField.value = playerScore;
    botScoreField.value = botScore;
}

function startGame() {
    fetch("resetScores");
    fetch("start");
    setScores(0, 0);
    startAudio.play();
    backgroundAudio.play();
    gameStopped = false;
    startTimer(gameTime);
};

function stopGame() {
    fetch("stop");
    backgroundAudio.pause();
    backgroundAudio.currentTime = 0;
    gameStopped = true;
};

function startTimer(duration) {
    let timer = duration;
    let minutes, seconds;
    let intervalId;

    intervalId = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        countdown.value = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
        }

        if (gameStopped) {
            clearInterval(intervalId);
        }
    }, 1000);
};

function playGIF(player) {
    const gifElement = document.getElementById('score-gif');
    const scoreboard = document.getElementById('scoreboard');

    if (player === 'prof') {
        gifElement.src = 'resources/gifs/pulp.gif';
    } else if (player === 'bot') {
        gifElement.src = 'resources/gifs/losingteeth.gif';
    }

    scoreboard.style.display = 'block';

    setTimeout(() => {
        scoreboard.style.display = 'none';
    }, 3000);
};

function animation() {
    fetch("animation");
};
