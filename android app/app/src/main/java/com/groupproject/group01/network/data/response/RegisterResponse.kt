package com.groupproject.group01.network.data.response

import com.google.gson.annotations.SerializedName

data class User(
    @SerializedName("email")
    val email: String,
    @SerializedName("firstname")
    val firstname: String,
    @SerializedName("lastname")
    val lastname: String,
    @SerializedName("phonenumber")
    val phonenumber: String
)

data class RegisterResponse(
    @SerializedName("User")
    val user: User
)

