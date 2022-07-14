const APP_ID = "58856723c6cb4b1bb645bc976a5b286b"
const CHANNEL = "main"
const TOKEN = "00658856723c6cb4b1bb645bc976a5b286bIABsGVR6n4mQPTrHD6GA252y2+k6b7kTe1jjn8ZvgJj92mTNKL8AAAAAEAC3KIpZ+eBxYgEAAQD44HFi"
let UID;
//thanks to agora.io for this beautiful video app
const client = AgoraRTC.createClient({
    mode:'rtc',codec:'vp8'
})
let localTracks= []
let remoteUsers  = {}

let joinAndDisplayLocalStream = async () => {
    // if the client is true they call the user-published and the handle user joined
    client.on('user-published',handleUserJoined)
    //left 
    client.on('user-left', handleUserLeft)
    UID = await client.join(APP_ID, CHANNEL, TOKEN, null)

    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()


    let player = `<div class="video-container" id="user-container-${UID}">
                    <div class="username-wrapper"><span class="user-name">My name</span></div>
                    <div class="video-player" id="user-${UID}"></div>
                </div>`
    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)

    localTracks[1].play(`user-${UID}`)

    await client.publish([localTracks[0], localTracks[1]])


}
let handleUserJoined = async(user, mediaType) => {
    remoteUsers[user.uid] = user
    //subcribe to remote user
    await client.subscribe(user,mediaType)
    //video append in the player html file
    if(mediaType== 'video'){
        let player = document.getElementById(`user-container-${user.uid}`)
        if(player != null){
            player.remove()

        }
        player = `<div class="video-container" id="user-container-${user.uid}">
                        <div class="username-wrapper"><span class="user-name">My name</span></div>
                        <div class="video-player" id="user-${user.uid}"></div>
                    </div>`
        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
        user.videoTrack.play(`user-${user.uid}`)
    }
    // playing the audio track
    if (mediaType == 'audio'){
        user.audioTrack.play()

    }
}
//deleting user in the video chat
let handleUserLeft = async (user) => {
    delete remoteUsers[user.id]
    document.getElementById(`user-container-${user.uid}`).remove()
}
//for loop in leave and remove
let leaveAndRemoveLocalStream = async () => {
    for(let i=0; localTracks.length > i; i++){
        localTracks[i].stop()
        localTracks[i].close()
    }
    await client.leave()
    window.open('/lobby/','_self')

}
joinAndDisplayLocalStream()
//getting the leave-btn id in the html and add to event listener to click it
document.getElementById('leave-btn').addEventListener('click', leaveAndRemoveLocalStream)
