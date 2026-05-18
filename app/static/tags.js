const MAX_TAGS = 5

function renderSelectedTags(data) {

    const selectedCount =
        document.getElementById(
            "selected_count"
        )

    if (selectedCount) {

        selectedCount.textContent =
            data.count

    }

    const container =
        document.getElementById(
            "selected_tags_container"
        )

    if (!container) {

        return

    }

    container.innerHTML = ""

    data.tags.forEach(tagData => {

        const div =
            document.createElement(
                "div"
            )

        div.classList.add(
            "selected_tag"
        )

        div.dataset.id =
            tagData.id

        div.innerHTML = `

            ${tagData.name}

            <span class="remove_tag">
                ✕
            </span>

        `

        container.appendChild(
            div
        )

    })

}

function setupTags() {

    const tags =
        document.querySelectorAll(".tag")

    tags.forEach(tag => {

        tag.onclick = async () => {

            const alreadyActive =
                tag.classList.contains(
                    "active"
                )

            const activeTags =
                document.querySelectorAll(
                    ".tag.active"
                )

            if (
                !alreadyActive &&
                activeTags.length >= MAX_TAGS
            ) {

                alert(
                    `You can only select ${MAX_TAGS} tags`
                )

                return

            }

            const tagId =
                tag.dataset.id

            const response =
                await fetch(
                    `/toggle_tag/${tagId}`
                )

            const data =
                await response.json()

            if (data.error === "limit") {

                return

            }

            if (alreadyActive) {

                tag.classList.remove(
                    "active"
                )

            }

            else {

                tag.classList.add(
                    "active"
                )

            }

            renderSelectedTags(data)

            await updateRecommendedGames()

        }

    })

}

document.addEventListener(
    "click",
    async event => {

        const removeButton =
            event.target.closest(
                ".remove_tag"
            )

        if (!removeButton) {

            return

        }

        const selectedTag =
            removeButton.closest(
                ".selected_tag"
            )

        const tagId =
            selectedTag.dataset.id

        const response =
            await fetch(
                `/toggle_tag/${tagId}`
            )

        const data =
            await response.json()

        const pageTag =
            document.querySelector(
                `.tag[data-id="${tagId}"]`
            )

        if (pageTag) {

            pageTag.classList.remove(
                "active"
            )

        }

        renderSelectedTags(data)

        await updateRecommendedGames()

    }
)

async function updateRecommendedGames() {

    const recommendedGames =
        document.getElementById(
            "recommended_games"
        )

    const noGamesText =
        document.getElementById(
            "no_games_text"
        )

    if (!recommendedGames) {

        return

    }

    const response =
        await fetch(
            "/recommended_games_data"
        )

    const games =
        await response.json()

    recommendedGames.innerHTML = ""

    const gameIds =
        Object.keys(games)

    if (gameIds.length === 0) {

        recommendedGames.innerHTML = `

            <p class="no_recommended_games">
                ${noGamesText.value}
            </p>

        `

        return

    }

    for (const gameId of gameIds) {

        const game = games[gameId]

        recommendedGames.innerHTML += `

            <a
                href="/show_game/${gameId}"
                class="recommended_game_card"
            >

                <img
                    src="${game.image}"
                    alt="${game.name}"
                >

                <span>
                    ${game.name}
                </span>

            </a>

        `

    }

}