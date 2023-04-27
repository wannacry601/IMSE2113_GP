package com.groupproject.group01.viewmodels

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.groupproject.group01.domain.usecases.LoginUseCase
import com.groupproject.group01.domain.usecases.RegisterUserUseCase
import com.groupproject.group01.network.data.requests.LoginRequest
import com.groupproject.group01.network.data.requests.RegisterRequest
import com.groupproject.group01.network.data.response.LoginResponse
import com.groupproject.group01.network.data.response.RegisterResponse
import com.groupproject.group01.util.Resource
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import javax.inject.Inject

class RegisterState (
    var isLoading:Boolean = false,
    var data: RegisterResponse? = null,
    var error: String = ""
)

class LoginState (
    var isLoading:Boolean = false,
    var data: LoginResponse? = null,
    var error: String = ""
)

@HiltViewModel
class AuthViewModel @Inject constructor(
    private val registerUserUseCase: RegisterUserUseCase,
    private val loginUseCase: LoginUseCase
) : ViewModel() {
    private val registerState: MutableLiveData<RegisterState> = MutableLiveData()
    val _registerState: LiveData<RegisterState>
        get() = registerState

    private val loginState: MutableLiveData<LoginState> = MutableLiveData()
    val _loginState: LiveData<LoginState>
        get() = loginState

    fun register(registerRequest: RegisterRequest){
        registerUserUseCase(registerRequest).onEach { result->
            when(result){
                is Resource.Success ->{
                    registerState.value = RegisterState(data = result.data)
                }
                is Resource.Loading ->{
                    registerState.value = RegisterState(isLoading = true)
                }
                is Resource.Error -> {
                    registerState.value = result.message?.let { RegisterState(error = it) }
                }
            }
        }.launchIn(viewModelScope)
    }

    fun login(loginRequest: LoginRequest){
        loginUseCase(loginRequest).onEach { result ->
            when(result){
                is Resource.Success ->{
                    loginState.value = LoginState(data = result.data)
                }

                is Resource.Loading -> {
                    loginState.value = LoginState(isLoading = true)
                }

                is Resource.Error -> {
                    loginState.value = result.message?.let { LoginState(error = it) }
                }
            }
        }.launchIn(viewModelScope)
    }
}