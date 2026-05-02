package com.estore.customer.controller;

import com.estore.customer.dto.UpdateUserDto;
import com.estore.customer.dto.UserDetailsDto;
import com.estore.customer.service.UserService;
import com.estore.shared.ApiResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping("/me")
    public ResponseEntity<ApiResponse<UserDetailsDto>> me() {
        return ResponseEntity.ok(ApiResponse.ok(userService.me()));
    }

    @PutMapping("/me")
    public ResponseEntity<ApiResponse<UserDetailsDto>> updateMe(@Valid @RequestBody UpdateUserDto dto) {
        return ResponseEntity.ok(ApiResponse.ok("Profil mis à jour", userService.updateMe(dto)));
    }
}
