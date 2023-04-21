package com.groupproject.group01.depinj

import android.content.Context
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.groupproject.group01.network.data.AuthyApi
import com.groupproject.group01.util.Constant.BASE_URL
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
class ApplicationModule {
    @Singleton
    @Provides
    fun provideGsonBuilder(): Gson {//This dependency allows the conversion of Kotlin data objects into JSON and vice versa.
        return GsonBuilder()
            .create()
    }

    @Singleton
    @Provides
    fun provideRetrofit(
        gson: Gson,
        okHttpClient: OkHttpClient
    ): Retrofit.Builder { // Retrofit is used to make network class to the remote API.
        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create(gson))
            .client(okHttpClient)
    }

    @Singleton
    @Provides
    // The API service comes from our instance of the API built using Retrofit.
    // We initialize it here to be used across the entire application.
    fun provideAuthyService(retrofit: Retrofit.Builder): AuthyApi {
        return retrofit
            .build()
            .create(AuthyApi::class.java)
    }

    @Singleton
    @Provides
    // The interceptor intercepts the API request and logs the responses on the console.
    // The procedure is essential for debugging and determining the causes of the error that made a request fail.
    fun provideInterceptor(
        @ApplicationContext context: Context,
    ): OkHttpClient {
        val interceptor = HttpLoggingInterceptor().setLevel(HttpLoggingInterceptor.Level.BODY)
        return OkHttpClient.Builder()
            .addInterceptor(interceptor)
            .build()
    }
}