export interface SearchMusicResult {
    code: number
    list: SearchMusicResultSingle[]
    page: Page
}

export interface SearchMusicResultSingle {
    album: string
    extra: string
    mid: string
    musicid: number
    notice: string
    prefix: string
    readableText: string
    singer: string
    size: number
    songmid: string
    time_publish: string
    title: string
}

export interface Page {
    cur: number
    next: number
    searchKey: string
    size: number
}


export interface InitAnonimous {
    code: number
    cookie: string
    createTime: number
    userId: number
}

export interface MediaQuery {
    meta_support: string,
    meta_option: string,
    meta_types: string,
    from: string,
    to: string
}