package com.ruoyi.guestHotel.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.ruoyi.guestHotel.domain.Scenicareas;
import com.ruoyi.guestHotel.mapper.ScenicareasMapper;
import com.ruoyi.guestHotel.service.ScenicareasService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

/**
 * @author 86176
 * @description 针对表【scenicareas】的数据库操作Service实现
 * @createDate 2024-07-17 09:44:30
 */
@Service
public class ScenicareasServiceImpl extends ServiceImpl<ScenicareasMapper, Scenicareas>
        implements ScenicareasService {

    @Resource
    private ScenicareasMapper scenicareasMapper;

    @Override
    public List<Scenicareas> findAllScenicareas() {
        return scenicareasMapper.getList();
    }
}




