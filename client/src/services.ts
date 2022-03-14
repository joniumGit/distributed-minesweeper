import axios from "axios";

interface Settings {
    width: number
    height: number
    mines: number
    nodeUrl?: string
    auth?: string
    field?: Array<Array<number>>
}

interface API extends Settings {
    reserveNode: () => Promise<any>
    startGame: () => Promise<any>
    waitInit: () => Promise<any>
    setters: any
}

async function sleep(millis: number) {
    await new Promise(r => setTimeout(r, millis))
}

async function getStatus(url: string, auth: string) {
    let r = await axios.get(url, {
        headers: {
            authorization: auth
        }
    })
    return r.status
}

function getAPI(settings: Settings, setters: any): API {
    return {
        ...settings,
        setters: setters,
        reserveNode: async function reserveNode() {
            let r = await axios.post('http://localhost/start', {})
            this.nodeUrl = r.headers.location
            this.auth = r.headers.authorization
            await sleep(1000)
            for (let i = 0; i < 100; i++) {
                r = await axios.post(this.nodeUrl, null, {validateStatus: () => true})
                if (r.status === 403) {
                    return
                }
                await sleep(500)
            }
        },
        startGame: async function startGame() {
            if (!this.nodeUrl || !this.auth) {
                window.location.href = '/'
                return;
            }
            const query = `?width=${this.width}&height=${this.height}&mines=${this.mines}`;
            const r = await axios.post(this.nodeUrl + query, null, {
                headers: {
                    authorization: this.auth
                }
            })
            this.nodeUrl = r.headers.location
        },
        waitInit: async function waitInit() {
            if (!this.nodeUrl || !this.auth) {
                window.location.href = '/'
                return;
            }
            while (await getStatus(this.nodeUrl, this.auth) !== 200) {
                await sleep(500)
            }
        }
    }
}

export {getAPI}