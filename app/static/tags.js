const MAX_TAGS = 5

function setupTags() {

    const tags =
        document.querySelectorAll(".tag")

    tags.forEach(tag => {

        tag.addEventListener(
            "click",
            async () => {

                const activeTags =
                    document.querySelectorAll(
                        ".tag.active"
                    )

                const alreadyActive =
                    tag.classList.contains(
                        "active"
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

                tag.classList.toggle(
                    "active"
                )

                const tagId =
                    tag.dataset.id

                await fetch(
                    `/toggle_tag/${tagId}`
                )

                if (
                    document.getElementById(
                        "selected_tags_container"
                    ) &&
                    document.getElementById(
                        "selected_count"
                    )
                ) {

                    updateSelectedTagsUI()

                }

                if (
                    typeof updateSelectAllButton
                    === "function"
                ) {

                    updateSelectAllButton()

                }

            }
        )

    })

}