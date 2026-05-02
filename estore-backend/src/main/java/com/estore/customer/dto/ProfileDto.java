package com.estore.customer.dto;

import com.estore.customer.entity.Profile;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProfileDto {

    private String phone;
    private String address;
    private String city;
    private String country;

    public static ProfileDto from(Profile p) {
        if (p == null) return new ProfileDto();
        return ProfileDto.builder()
                .phone(p.getPhone())
                .address(p.getAddress())
                .city(p.getCity())
                .country(p.getCountry())
                .build();
    }
}
