package com.ruoyi.guestHotel.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.ruoyi.guestHotel.domain.Scenicspots;

import java.util.List;

/**
 * @author 86176
 * @description 针对表【scenicspots】的数据库操作Mapper
 * @createDate 2024-07-17 09:44:30
 * @Entity com.ruoyi.guestHotel.domain.Scenicspots
 */
public interface ScenicspotsMapper extends BaseMapper<Scenicspots> {
    List<Scenicspots> selectByScenicAreaId(String scenicAreaId);
}




