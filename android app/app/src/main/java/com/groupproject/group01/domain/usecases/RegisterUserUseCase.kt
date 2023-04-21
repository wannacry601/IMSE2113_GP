package com.groupproject.group01.domain.usecases

import com.groupproject.group01.domain.repository.AuthRepository
import com.groupproject.group01.network.data.requests.RegisterRequest
import com.groupproject.group01.network.data.response.RegisterResponse
import com.groupproject.group01.util.Resource
import kotlinx.coroutines.flow.flow
import retrofit2.HttpException
import java.io.IOException
import java.util.concurrent.Flow
import javax.inject.Inject

class RegisterUserUseCase @Inject constructor(private val repository: AuthRepository){
    operator fun invoke(request: RegisterRequest): kotlinx.coroutines.flow.Flow<Resource<RegisterResponse>> = flow {
        try {
            emit(Resource.Loading())
            val response = repository.register(request)
            emit(Resource.Success(response))
        }catch (e: HttpException){
            emit(Resource.Error("An error occurred"))
        }catch (e: IOException){
            emit(Resource.Error("Check internet connection"))
        }
    }
}