package com.ruoyi.guestHotel.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.ruoyi.guestHotel.domain.Scenicspots;
import com.ruoyi.guestHotel.service.ScenicspotsService;
import com.ruoyi.guestHotel.mapper.ScenicspotsMapper;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

/**
* @author 86176
* @description 针对表【scenicspots】的数据库操作Service实现
* @createDate 2024-07-17 09:44:30
*/
@Service
public class ScenicspotsServiceImpl extends ServiceImpl<ScenicspotsMapper, Scenicspots>
    implements ScenicspotsService{

    @Resource
    private ScenicspotsMapper scenicspotsMapper;

    @Override
    public List<Scenicspots> findScenicspotsByScenicAreaId(String scenicAreaId) {
        return scenicspotsMapper.selectByScenicAreaId(scenicAreaId);
    }
}




