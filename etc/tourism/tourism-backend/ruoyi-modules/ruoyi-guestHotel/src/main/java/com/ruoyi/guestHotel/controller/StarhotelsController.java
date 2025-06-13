package com.ruoyi.guestHotel.controller;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.guestHotel.domain.Starhotels;
import com.ruoyi.guestHotel.service.IStarhotelsService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 星级酒店Controller
 * 
 * @author ruoyi
 * @date 2024-07-06
 */
@RestController
@RequestMapping("/guest/starhotels")
public class StarhotelsController extends BaseController
{
    @Autowired
    private IStarhotelsService starhotelsService;

    /**
     * 查询星级酒店列表
     */

    @GetMapping("/list")
    public TableDataInfo list(Starhotels starhotels)
    {
        startPage();
        List<Starhotels> list = starhotelsService.selectStarhotelsList(starhotels);
        return getDataTable(list);
    }


    /**
     * 获取星级酒店
     */

    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(starhotelsService.selectStarhotelsById(id));
    }
}
