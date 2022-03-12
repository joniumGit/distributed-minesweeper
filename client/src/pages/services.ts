interface Settings {
    width: number
    height: number
    mines: number
    nodeUrl: string
    auth: string
}

function getNode(settings: Settings, callback:any){
    let r = new window.XMLHttpRequest()
    r.onloadend = function() {
        settings.nodeUrl = this.getResponseHeader("Location")!
        settings.auth = this.getResponseHeader('Authorization')!;
        (async ()=>{
            await (new Promise(r=>setTimeout(r, 1000)));
            callback(settings)
        })()
    }
    r.open('POST', 'http://localhost/start')
    r.send()
}

function startGame(settings: Settings, callback:any){
    let r = new window.XMLHttpRequest()
    r.onloadend = function() {
        settings.nodeUrl = this.getResponseHeader("Location")!
        callback(settings)
    }
    const query = `?width=${settings.width}&height=${settings.height}&mines=${settings.mines}`;
    r.open('POST', settings.nodeUrl+query)
    r.setRequestHeader('Authorization', settings.auth)
    r.send()
}

function waitGame(settings: Settings, callback:any){
    let r = new window.XMLHttpRequest()
    r.onloadend = function() {
        if (this.status !== 200){
            (async ()=>{
                await (new Promise(r=>setTimeout(r, 1000)));
                waitGame(settings, callback)
            })()
        }else{
            callback(settings)
        }
    }
    r.open('GET', settings.nodeUrl)
    r.setRequestHeader('Authorization', settings.auth)
    r.send()
}

export {getNode, startGame, waitGame}