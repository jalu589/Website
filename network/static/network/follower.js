function like_post(post) {
    console.log(post, 'liked')
    const likeButton = document.querySelector(`#like-button-${post}`)
    fetch(`/network/like/${post}`, {
        method: 'PUT'
    })
    .catch(error => {
        console.log('Error: ', error)
    });
    location.reload()
}