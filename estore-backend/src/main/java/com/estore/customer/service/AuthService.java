package com.estore.customer.service;

import com.estore.customer.dto.AuthResponseDto;
import com.estore.customer.dto.LoginDto;
import com.estore.customer.dto.RegisterDto;
import com.estore.customer.dto.UserDto;
import com.estore.customer.entity.Profile;
import com.estore.customer.entity.Role;
import com.estore.customer.entity.User;
import com.estore.customer.repository.UserRepository;
import com.estore.customer.security.JwtService;
import com.estore.exception.BusinessException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Inscription et connexion.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final AuthenticationManager authenticationManager;

    /**
     * Inscrit un nouvel utilisateur. Crée un profil vide associé.
     */
    @Transactional
    public AuthResponseDto register(RegisterDto dto) {
        if (userRepository.existsByEmail(dto.getEmail())) {
            throw new BusinessException("Cet email est déjà utilisé");
        }
        User user = User.builder()
                .firstName(dto.getFirstName())
                .lastName(dto.getLastName())
                .email(dto.getEmail())
                .password(passwordEncoder.encode(dto.getPassword()))
                .role(Role.USER)
                .build();

        Profile profile = Profile.builder().user(user).build();
        user.setProfile(profile);

        User saved = userRepository.save(user);
        log.info("Nouvel utilisateur inscrit : {}", saved.getEmail());

        String token = jwtService.generateToken(saved);
        return AuthResponseDto.builder()
                .token(token)
                .user(UserDto.from(saved))
                .build();
    }

    /**
     * Authentifie l'utilisateur et renvoie un JWT.
     */
    public AuthResponseDto login(LoginDto dto) {
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(dto.getEmail(), dto.getPassword())
        );
        User user = userRepository.findByEmail(dto.getEmail())
                .orElseThrow(() -> new BusinessException("Email introuvable"));

        String token = jwtService.generateToken(user);
        return AuthResponseDto.builder()
                .token(token)
                .user(UserDto.from(user))
                .build();
    }
}
