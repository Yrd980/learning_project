package com.ruoyi.guestHotel.controller;

import com.ruoyi.guestHotel.common.BaseResponse;
import com.ruoyi.guestHotel.common.ResultUtils;
import com.ruoyi.guestHotel.domain.Scenicareas;
import com.ruoyi.guestHotel.domain.Scenicspots;
import com.ruoyi.guestHotel.service.ScenicareasService;
import com.ruoyi.guestHotel.service.ScenicspotsService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import java.util.List;

/**
 * @className ScenicController
 * @description:
 * @author yrd
 * @since 7/17/2024 9:50 AM
 * @version 1.0
 */

@RestController
@RequestMapping("/scenic")
public class ScenicController {
    @Resource
    private ScenicareasService scenicareasService;
    @Resource
    private ScenicspotsService scenicspotsService;

    @GetMapping("/scenicArea/list")
    public BaseResponse<List<Scenicareas>> getScenicareas() {
        List<Scenicareas> scenicareasList = scenicareasService.findAllScenicareas();
        return ResultUtils.success(scenicareasList);
    }

    @GetMapping("/scenicSpots/list")
    public BaseResponse<List<Scenicspots>> getScenicspots(@RequestParam String scenicAreaId) {
        List<Scenicspots> scenicspotsList = scenicspotsService.findScenicspotsByScenicAreaId(scenicAreaId);
        return ResultUtils.success(scenicspotsList);
    }


}
