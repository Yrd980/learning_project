package com.ruoyi.guestHotel.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.ruoyi.guestHotel.domain.Scenicspots;

import java.util.List;

/**
* @author 86176
* @description 针对表【scenicspots】的数据库操作Service
* @createDate 2024-07-17 09:44:30
*/
public interface ScenicspotsService extends IService<Scenicspots> {

    List<Scenicspots> findScenicspotsByScenicAreaId(String scenicAreaId);
}
