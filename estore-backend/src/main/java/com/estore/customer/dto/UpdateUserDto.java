package com.estore.customer.dto;

import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class UpdateUserDto {

    @Size(max = 80)
    private String firstName;

    @Size(max = 80)
    private String lastName;

    private ProfileDto profile;
}
