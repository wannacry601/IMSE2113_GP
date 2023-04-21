package com.groupproject.group01.domain.repository

import com.groupproject.group01.network.data.AuthyApi
import com.groupproject.group01.network.data.requests.LoginRequest
import com.groupproject.group01.network.data.requests.RegisterRequest
import com.groupproject.group01.network.data.response.LoginResponse
import com.groupproject.group01.network.data.response.RegisterResponse
import javax.inject.Inject

class AuthRepository @Inject constructor(
    private val api: AuthyApi
) {
    suspend fun register(request: RegisterRequest): RegisterResponse = api.register(request)
    suspend fun login(request: LoginRequest): LoginResponse = api.login(request)
}