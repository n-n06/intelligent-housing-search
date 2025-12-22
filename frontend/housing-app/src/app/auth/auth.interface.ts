export interface TokenResponse {
    access_token: string,
    token_type: string
}

export interface UserLogin {
    username: string,
    password: string
}

export interface UserRegistration extends UserLogin {
    email: string,
    password2: string
}
