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
            let r = await axios.get(this.nodeUrl, {
                headers: {
                    authorization: this.auth
                }
            })
            if (r.status !== 200) {
                await sleep(500)
                await waitInit()
            }
        }
    }
}

export {getAPI}