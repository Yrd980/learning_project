package com.ruoyi.guestHotel.service.impl;

import com.ruoyi.guestHotel.domain.Complaints;
import com.ruoyi.guestHotel.mapper.ComplaintsMapper;
import com.ruoyi.guestHotel.service.IComplaintsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ComplaintsServiceImpl implements IComplaintsService {
    @Autowired
    private ComplaintsMapper complaintsMapper;

    @Override
    public List<Complaints> selectComplaintsById(Long id) {
        return complaintsMapper.selectComplaintsById(id);
    }

}
