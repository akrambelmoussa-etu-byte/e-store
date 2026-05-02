package com.estore.customer.controller;

import com.estore.customer.dto.AuthResponseDto;
import com.estore.customer.dto.LoginDto;
import com.estore.customer.dto.RegisterDto;
import com.estore.customer.service.AuthService;
import com.estore.shared.ApiResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @PostMapping("/register")
    public ResponseEntity<ApiResponse<AuthResponseDto>> register(@Valid @RequestBody RegisterDto dto) {
        AuthResponseDto resp = authService.register(dto);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.ok("Inscription réussie", resp));
    }

    @PostMapping("/login")
    public ResponseEntity<ApiResponse<AuthResponseDto>> login(@Valid @RequestBody LoginDto dto) {
        AuthResponseDto resp = authService.login(dto);
        return ResponseEntity.ok(ApiResponse.ok("Connexion réussie", resp));
    }
}
