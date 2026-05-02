package com.estore.customer.service;

import com.estore.customer.dto.ProfileDto;
import com.estore.customer.dto.UpdateUserDto;
import com.estore.customer.dto.UserDetailsDto;
import com.estore.customer.entity.Profile;
import com.estore.customer.entity.User;
import com.estore.customer.repository.UserRepository;
import com.estore.customer.security.SecurityUtils;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Gestion du compte utilisateur courant.
 */
@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final SecurityUtils securityUtils;

    @Transactional(readOnly = true)
    public UserDetailsDto me() {
        User u = securityUtils.currentUser();
        // Force le chargement du profile (lazy)
        if (u.getProfile() != null) u.getProfile().getId();
        return UserDetailsDto.from(u);
    }

    @Transactional
    public UserDetailsDto updateMe(UpdateUserDto dto) {
        User u = securityUtils.currentUser();
        if (dto.getFirstName() != null) u.setFirstName(dto.getFirstName());
        if (dto.getLastName() != null) u.setLastName(dto.getLastName());

        ProfileDto p = dto.getProfile();
        if (p != null) {
            Profile profile = u.getProfile();
            if (profile == null) {
                profile = Profile.builder().user(u).build();
                u.setProfile(profile);
            }
            profile.setPhone(p.getPhone());
            profile.setAddress(p.getAddress());
            profile.setCity(p.getCity());
            profile.setCountry(p.getCountry());
        }

        User saved = userRepository.save(u);
        return UserDetailsDto.from(saved);
    }
}
