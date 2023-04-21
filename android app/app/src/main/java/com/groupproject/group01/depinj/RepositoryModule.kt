package com.groupproject.group01.depinj

import com.groupproject.group01.domain.repository.AuthRepository
import com.groupproject.group01.network.data.AuthyApi
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
class RepositoryModule {
    @Singleton
    @Provides
    fun provideAuthRepository(api: AuthyApi): AuthRepository = AuthRepository(api)
}