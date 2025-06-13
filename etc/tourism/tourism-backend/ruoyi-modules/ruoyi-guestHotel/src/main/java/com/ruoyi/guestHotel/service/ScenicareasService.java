package com.ruoyi.guestHotel.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.ruoyi.guestHotel.domain.Scenicareas;

import java.util.List;

/**
 * @author 86176
 * @description 针对表【scenicareas】的数据库操作Service
 * @createDate 2024-07-17 09:44:30
 */
public interface ScenicareasService extends IService<Scenicareas> {

    List<Scenicareas> findAllScenicareas();
}
