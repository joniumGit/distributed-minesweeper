import axios from "axios";

interface Square {
    x: number
    y: number
    flag?: boolean
    mine?: boolean
    open?: boolean
    value?: number
}

interface Settings {
    width: number
    height: number
    mines: number
    nodeUrl?: string
    auth?: string
    field?: Array<Array<number | string>>
}

interface Setters {
    width: (e: Event) => void,
    height: (e: Event) => void,
    mines: (e: Event) => void,
    update: (o: Settings) => void
}

interface API extends Settings {
    reserveNode: () => Promise<any>
    startGame: () => Promise<any>
    waitInit: () => Promise<any>
    updateField: (items: Square[]) => Promise<any>
    setters: Setters
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

export function openSquare(x: number, y: number, state: API) {
    (async () => {
        if (!state.nodeUrl || !state.auth) {
            window.location.href = '/'
            return;
        }
        const query = `open?x=${x}&y=${y}`;
        const r = await axios.post(state.nodeUrl + query, null, {
            headers: {
                authorization: state.auth
            }
        })
        if (r.data.items) {
            await state.updateField(r.data.items)
        }
        if ( r.data.status ) {
            (async () => {
                window.alert(r.data.status)
                await sleep(20000)
                window.location.href = '/'
            })()
        }
    })();
}

export function start(state: API, nav: any) {
    (async () => {
        await state.reserveNode()
        await state.startGame()
        await state.waitInit()
        nav('/game')
    })();
}

function getAPI(settings: Settings, setters: any): API {
    return {
        ...settings,
        setters: setters,
        reserveNode: async function reserveNode() {
            if( this.nodeUrl ) return
            let r = await axios.post('http://localhost/start', {})
            this.nodeUrl = r.headers.location
            this.auth = r.headers.authorization
            await sleep(1000)
            for (let i = 0; i < 100; i++) {
                r = await axios.post(this.nodeUrl, null, { validateStatus: () => true })
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
            if( this.field ) return
            const query = `?width=${this.width}&height=${this.height}&mines=${this.mines}`;
            const r = await axios.post(this.nodeUrl + query, null, {
                headers: {
                    authorization: this.auth
                }
            })
            this.nodeUrl = r.headers.location
            //initiate field
            const columns = []
            for (let i = 0; i < this.height; i++) {
                const rows = [];
                for (let j = 0; j < this.width; j++) {
                    rows.push(-1)
                }
                columns.push(rows)
            }
            this.field = columns
        },
        waitInit: async function waitInit() {
            if (!this.nodeUrl || !this.auth) {
                window.location.href = '/'
                return;
            }
            while (await getStatus(this.nodeUrl, this.auth) !== 200) {
                await sleep(500)
            }
            this.setters.update(this)
        },
        updateField: async function updateField(items: Square[]) {
            if (!this.field) {
                window.location.href = '/'
                return;
            }
            for (let i = 0; i < items.length; i++) {
                const item = items[i]
                let value
                if (item.flag) {
                    value = 'F'
                }
                else if (item.mine) {
                    value = 'X'
                }
                else if (item.value) {
                    value = item.value
                }
                else if (item.open) {
                    value = ''
                } else {
                    value = -1
                }
                this.field[item.y][item.x] = value
            }
            this.setters.update(this)
        }
    }
}

export { getAPI }