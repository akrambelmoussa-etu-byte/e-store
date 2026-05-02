package com.estore.catalog.service;

import com.estore.catalog.dto.CategoryDto;
import com.estore.catalog.entity.Category;
import com.estore.catalog.repository.CategoryRepository;
import com.estore.exception.BusinessException;
import com.estore.exception.ResourceNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class CategoryService {

    private final CategoryRepository categoryRepository;

    @Transactional(readOnly = true)
    public List<CategoryDto> findAll() {
        return categoryRepository.findAll().stream().map(CategoryDto::from).toList();
    }

    @Transactional(readOnly = true)
    public CategoryDto findById(Long id) {
        return CategoryDto.from(get(id));
    }

    @Transactional
    public CategoryDto create(CategoryDto dto) {
        if (categoryRepository.existsByNameIgnoreCase(dto.getName())) {
            throw new BusinessException("Une catégorie portant ce nom existe déjà");
        }
        Category c = Category.builder()
                .name(dto.getName())
                .description(dto.getDescription())
                .build();
        return CategoryDto.from(categoryRepository.save(c));
    }

    @Transactional
    public CategoryDto update(Long id, CategoryDto dto) {
        Category c = get(id);
        c.setName(dto.getName());
        c.setDescription(dto.getDescription());
        return CategoryDto.from(categoryRepository.save(c));
    }

    @Transactional
    public void delete(Long id) {
        Category c = get(id);
        categoryRepository.delete(c);
    }

    private Category get(Long id) {
        return categoryRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Catégorie introuvable : " + id));
    }
}
