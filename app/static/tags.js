const MAX_TAGS = 5

function setupTags() {

    const tags =
        document.querySelectorAll(".tag")

    tags.forEach(tag => {

        tag.onclick = async () => {

            const alreadyActive =
                tag.classList.contains(
                    "active"
                )

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

            const tagId =
                tag.dataset.id

            const response =
                await fetch(
                    `/toggle_tag/${tagId}`
                )

            const data =
                await response.json()

            if (data.error === "limit") {

                tag.classList.remove(
                    "active"
                )

                alert(
                    `You can only select ${MAX_TAGS} tags`
                )

                return

            }

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

            if (container) {

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

        if (!removeButton) return

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

        if (container) {

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

    }
)