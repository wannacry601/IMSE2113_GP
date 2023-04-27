package com.groupproject.group01.network.data

import com.groupproject.group01.network.data.requests.LoginRequest
import com.groupproject.group01.network.data.requests.RegisterRequest
import com.groupproject.group01.network.data.response.LoginResponse
import com.groupproject.group01.network.data.response.RegisterResponse
import retrofit2.http.Body
import retrofit2.http.POST

interface AuthyApi {
    companion object{
        const val REGISTER = "register/"
        const val LOGIN = "login/"
    }

    @POST(REGISTER)
    suspend fun register(@Body registerRequest: RegisterRequest): RegisterResponse

    @POST(LOGIN)
    suspend fun login(@Body loginRequest: LoginRequest): LoginResponse
}