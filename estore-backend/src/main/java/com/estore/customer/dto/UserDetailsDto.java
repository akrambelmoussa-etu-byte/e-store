package com.estore.customer.dto;

import com.estore.customer.entity.User;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * UserDto enrichi avec le profil. Utilisé par GET /api/users/me.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserDetailsDto {

    private UserDto user;
    private ProfileDto profile;

    public static UserDetailsDto from(User u) {
        return UserDetailsDto.builder()
                .user(UserDto.from(u))
                .profile(ProfileDto.from(u.getProfile()))
                .build();
    }
}
