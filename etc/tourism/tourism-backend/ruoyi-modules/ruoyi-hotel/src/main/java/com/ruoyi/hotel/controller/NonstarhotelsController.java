package com.ruoyi.hotel.controller;

import java.util.List;
import java.io.IOException;
import javax.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.log.annotation.Log;
import com.ruoyi.common.log.enums.BusinessType;
import com.ruoyi.common.security.annotation.RequiresPermissions;
import com.ruoyi.hotel.domain.Nonstarhotels;
import com.ruoyi.hotel.service.INonstarhotelsService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 非星级酒店Controller
 * 
 * @author ningf
 * @date 2024-07-14
 */
@RestController
@RequestMapping("/nonstarhotels")
public class NonstarhotelsController extends BaseController
{
    @Autowired
    private INonstarhotelsService nonstarhotelsService;

    /**
     * 查询非星级酒店列表
     */
    @RequiresPermissions("hotel:nonstarhotels:list")
    @GetMapping("/list")
    public TableDataInfo list(Nonstarhotels nonstarhotels)
    {
        startPage();
        List<Nonstarhotels> list = nonstarhotelsService.selectNonstarhotelsList(nonstarhotels);
        return getDataTable(list);
    }

    /**
     * 导出非星级酒店列表
     */
    @RequiresPermissions("hotel:nonstarhotels:export")
    @Log(title = "非星级酒店", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Nonstarhotels nonstarhotels)
    {
        List<Nonstarhotels> list = nonstarhotelsService.selectNonstarhotelsList(nonstarhotels);
        ExcelUtil<Nonstarhotels> util = new ExcelUtil<Nonstarhotels>(Nonstarhotels.class);
        util.exportExcel(response, list, "非星级酒店数据");
    }

    /**
     * 获取非星级酒店详细信息
     */
    @RequiresPermissions("hotel:nonstarhotels:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(nonstarhotelsService.selectNonstarhotelsById(id));
    }

    /**
     * 新增非星级酒店
     */
    @RequiresPermissions("hotel:nonstarhotels:add")
    @Log(title = "非星级酒店", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Nonstarhotels nonstarhotels)
    {
        return toAjax(nonstarhotelsService.insertNonstarhotels(nonstarhotels));
    }

    /**
     * 修改非星级酒店
     */
    @RequiresPermissions("hotel:nonstarhotels:edit")
    @Log(title = "非星级酒店", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Nonstarhotels nonstarhotels)
    {
        return toAjax(nonstarhotelsService.updateNonstarhotels(nonstarhotels));
    }

    /**
     * 删除非星级酒店
     */
    @RequiresPermissions("hotel:nonstarhotels:remove")
    @Log(title = "非星级酒店", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(nonstarhotelsService.deleteNonstarhotelsByIds(ids));
    }
}
