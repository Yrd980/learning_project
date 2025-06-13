package com.ruoyi.guestHotel.controller;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.guestHotel.domain.Nonstarhotels;
import com.ruoyi.guestHotel.service.INonstarhotelsService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 非星级酒店Controller
 * 
 * @author ruoyi
 * @date 2024-07-11
 */
@RestController
@RequestMapping("/guest/nonstarhotels")
public class NonstarhotelsController extends BaseController
{
    @Autowired
    private INonstarhotelsService nonstarhotelsService;

    /**
     * 查询非星级酒店列表
     */

    @GetMapping("/list")
    public TableDataInfo list(Nonstarhotels nonstarhotels)
    {
        startPage();
        List<Nonstarhotels> list = nonstarhotelsService.selectNonstarhotelsList(nonstarhotels);
        return getDataTable(list);
    }



    /**
     * 获取非星级酒店详细信息
     */

    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(nonstarhotelsService.selectNonstarhotelsById(id));
    }
}
